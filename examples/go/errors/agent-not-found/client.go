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
	agentID   = "nonexistent-agent"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/send",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Hello?"}},
			},
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

	errorObj, _ := result["error"].(map[string]interface{})
	code, _ := errorObj["code"].(float64)
	msg, _ := errorObj["message"].(string)
	fmt.Printf("\nError code:    %.0f\n", code)
	fmt.Printf("Error message: %s\n", msg)

	if int(code) != -32002 {
		fmt.Fprintf(os.Stderr, "Expected -32002, got %.0f\n", code)
		os.Exit(1)
	}
	fmt.Println("\nAgent-not-found error (-32002) received as expected!")
}
