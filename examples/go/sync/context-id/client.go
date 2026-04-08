package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "context-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/send",
		"params": map[string]interface{}{
			"message":   map[string]interface{}{"parts": []map[string]interface{}{{"text": "Track this request"}}},
			"contextId": "ctx-001",
		},
	}

	data, _ := json.Marshal(payload)
	resp, err := http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var pretty bytes.Buffer
	json.Indent(&pretty, body, "", "  ")
	fmt.Println(pretty.String())

	var result map[string]interface{}
	json.Unmarshal(body, &result)

	returnedCtx := ""
	if r, ok := result["result"].(map[string]interface{}); ok {
		if c, ok := r["contextId"].(string); ok {
			returnedCtx = c
		}
	}

	fmt.Printf("\nSent contextId:     ctx-001\n")
	fmt.Printf("Received contextId: %s\n", returnedCtx)

	if returnedCtx == "ctx-001" {
		fmt.Println("Context ID correlation verified!")
	} else {
		fmt.Println("Warning: contextId mismatch")
	}
}
