// Go drivers. One binary, two libraries:
//   ctgo go-sdk     github.com/modelcontextprotocol/go-sdk CommandTransport (Crush's transport)
//   ctgo mcp-go     github.com/mark3labs/mcp-go stdio client
// Connect, list tools, call ping, close; print CLOSED; stay alive until stdin closes.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"time"

	mcpgoclient "github.com/mark3labs/mcp-go/client"
	mcpgo "github.com/mark3labs/mcp-go/mcp"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type spec struct {
	Command string   `json:"command"`
	Args    []string `json:"args"`
}

func must(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func main() {
	var s spec
	must(json.Unmarshal([]byte(os.Getenv("CT_SPEC")), &s))
	ctx := context.Background()
	var secs float64
	switch os.Args[1] {
	case "go-sdk":
		client := mcp.NewClient(&mcp.Implementation{Name: "ct-driver", Version: "0"}, nil)
		sess, err := client.Connect(ctx, &mcp.CommandTransport{Command: exec.Command(s.Command, s.Args...)}, nil)
		must(err)
		_, err = sess.ListTools(ctx, nil)
		must(err)
		_, err = sess.CallTool(ctx, &mcp.CallToolParams{Name: "ping", Arguments: map[string]any{}})
		must(err)
		t := time.Now()
		_ = sess.Close()
		secs = time.Since(t).Seconds()
	case "mcp-go":
		c, err := mcpgoclient.NewStdioMCPClient(s.Command, nil, s.Args...)
		must(err)
		req := mcpgo.InitializeRequest{}
		req.Params.ProtocolVersion = mcpgo.LATEST_PROTOCOL_VERSION
		req.Params.ClientInfo = mcpgo.Implementation{Name: "ct-driver", Version: "0"}
		_, err = c.Initialize(ctx, req)
		must(err)
		_, err = c.ListTools(ctx, mcpgo.ListToolsRequest{})
		must(err)
		call := mcpgo.CallToolRequest{}
		call.Params.Name = "ping"
		_, err = c.CallTool(ctx, call)
		must(err)
		t := time.Now()
		_ = c.Close()
		secs = time.Since(t).Seconds()
	}
	fmt.Printf("CLOSED {\"close_seconds\": %.2f}\n", secs)
	io.Copy(io.Discard, os.Stdin)
}
