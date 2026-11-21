//! Rust driver for rmcp's TokioChildProcess.
//!   ctrust rmcp          plain tokio Command, as rmcp's own examples do
//!   ctrust goose-spawn   Goose's configure_subprocess: process_group(0) plus
//!                        PR_SET_PDEATHSIG (crates/oi-kit-agent/src/subprocess.rs)
//! Connect, list tools, call ping, cancel the service (rmcp's close path),
//! print CLOSED, stay alive until stdin closes.
use rmcp::{model::CallToolRequestParams, transport::TokioChildProcess, ServiceExt};
use std::io::Read;
use std::time::Instant;
use tokio::process::Command;

#[tokio::main]
async fn main() {
    let mode = std::env::args().nth(1).expect("mode");
    let spec: serde_json::Value = serde_json::from_str(&std::env::var("CT_SPEC").unwrap()).unwrap();
    let mut cmd = Command::new(spec["command"].as_str().unwrap());
    for a in spec["args"].as_array().unwrap() {
        cmd.arg(a.as_str().unwrap());
    }
    if mode == "goose-spawn" {
        cmd.process_group(0);
        let parent = unsafe { libc::getpid() };
        unsafe {
            cmd.pre_exec(move || {
                if libc::prctl(libc::PR_SET_PDEATHSIG, libc::SIGTERM) != 0 {
                    return Err(std::io::Error::last_os_error());
                }
                if libc::getppid() != parent {
                    return Err(std::io::Error::from_raw_os_error(libc::ESRCH));
                }
                Ok(())
            });
        }
    }
    let transport = TokioChildProcess::new(cmd).unwrap();
    let client = ().serve(transport).await.unwrap();
    client.list_all_tools().await.unwrap();
    client
        .call_tool(CallToolRequestParams::new("ping"))
        .await
        .unwrap();
    let t = Instant::now();
    let _ = client.cancel().await;
    println!("CLOSED {{\"close_seconds\": {:.2}}}", t.elapsed().as_secs_f64());
    let mut sink = Vec::new();
    let _ = std::io::stdin().read_to_end(&mut sink);
}
