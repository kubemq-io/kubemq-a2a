package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "echo-agent-01"
)

func main() {
	fmt.Println("=== Test 1: Invalid JSON ===")
	req, _ := http.NewRequest("POST", kubemqURL+"/a2a/"+agentID, strings.NewReader("{invalid json!!!}"))
	req.Header.Set("Content-Type", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()
	var data map[string]interface{}
	json.Unmarshal(body, &data)
	errorObj, _ := data["error"].(map[string]interface{})
	code, _ := errorObj["code"].(float64)
	fmt.Printf("  Code: %.0f (expected -32700)\n", code)
	fmt.Printf("  Message: %v\n", errorObj["message"])

	fmt.Println("\n=== Test 2: Missing method field ===")
	payload2, _ := json.Marshal(map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"params":  map[string]interface{}{},
	})
	resp, _ = http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(payload2))
	body, _ = io.ReadAll(resp.Body)
	resp.Body.Close()
	json.Unmarshal(body, &data)
	errorObj, _ = data["error"].(map[string]interface{})
	code, _ = errorObj["code"].(float64)
	fmt.Printf("  Code: %.0f (expected -32600)\n", code)
	fmt.Printf("  Message: %v\n", errorObj["message"])

	fmt.Println("\n=== Test 3: Bad jsonrpc version ===")
	payload3, _ := json.Marshal(map[string]interface{}{
		"jsonrpc": "1.0",
		"id":      1,
		"method":  "message/send",
		"params":  map[string]interface{}{},
	})
	resp, _ = http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(payload3))
	body, _ = io.ReadAll(resp.Body)
	resp.Body.Close()
	json.Unmarshal(body, &data)
	errorObj, _ = data["error"].(map[string]interface{})
	code, _ = errorObj["code"].(float64)
	fmt.Printf("  Code: %.0f (expected -32600)\n", code)
	fmt.Printf("  Message: %v\n", errorObj["message"])

	fmt.Println("\nAll invalid request errors demonstrated!")
}
