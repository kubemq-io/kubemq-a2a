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
	agentID   = "echo-agent-01"
)

func main() {
	resp, err := http.Get(kubemqURL + "/agents/" + agentID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("Status: %d\n", resp.StatusCode)

	var pretty bytes.Buffer
	json.Indent(&pretty, body, "", "  ")
	fmt.Println(pretty.String())

	var data map[string]interface{}
	json.Unmarshal(body, &data)

	if data["agent_id"] != agentID {
		fmt.Fprintf(os.Stderr, "agent_id mismatch\n")
		os.Exit(1)
	}
	if _, ok := data["registered_at"]; !ok {
		fmt.Fprintf(os.Stderr, "registered_at missing\n")
		os.Exit(1)
	}
	fmt.Println("\nAgent registration verified successfully!")
}
