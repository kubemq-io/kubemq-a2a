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
	agentID   = "custom-method-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "custom/action",
		"params":  map[string]interface{}{"data": "custom-payload"},
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

	r, _ := result["result"].(map[string]interface{})
	handledMethod, _ := r["handled_method"].(string)
	fmt.Printf("\nHandled method: %s\n", handledMethod)

	if handledMethod != "custom/action" {
		fmt.Fprintf(os.Stderr, "Expected custom/action, got %s\n", handledMethod)
		os.Exit(1)
	}
	fmt.Println("Custom method forwarded successfully!")
}
