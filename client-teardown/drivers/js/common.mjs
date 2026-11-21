// Shared by every JS driver: read the server spec, report CLOSED, then stay
// alive as a host would until the runner closes our stdin.
export const spec = JSON.parse(process.env.CT_SPEC);
export async function closed(extra = {}) {
    process.stdout.write('CLOSED ' + JSON.stringify(extra) + '\n');
    await new Promise(r => { process.stdin.on('end', r); process.stdin.on('close', r); process.stdin.resume(); });
    process.exit(0);
}
export const timed = async fn => { const t = Date.now(); await fn(); return (Date.now() - t) / 1000; };
