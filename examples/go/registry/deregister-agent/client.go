package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "deregister-agent-01"
)

func main() {
	fmt.Println("=== Verify agent exists ===")
	resp, err := http.Get(kubemqURL + "/agents/" + agentID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	resp.Body.Close()
	fmt.Printf("GET /agents/%s: %d\n", agentID, resp.StatusCode)

	fmt.Println("\n=== Deregister via POST ===")
	body, _ := json.Marshal(map[string]string{"agent_id": agentID})
	resp, err = http.Post(kubemqURL+"/agents/deregister", "application/json", bytes.NewReader(body))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Deregister POST failed: %v\n", err)
		os.Exit(1)
	}
	resp.Body.Close()
	fmt.Printf("POST /agents/deregister: %d\n", resp.StatusCode)

	resp, _ = http.Get(kubemqURL + "/agents/" + agentID)
	resp.Body.Close()
	fmt.Printf("GET /agents/%s after deregister: %d\n", agentID, resp.StatusCode)

	fmt.Println("\n=== Re-register for DELETE test ===")
	card, _ := json.Marshal(map[string]interface{}{
		"agent_id":           agentID,
		"name":               "Deregister Test Agent",
		"url":                "http://localhost:18080/",
		"skills":             []interface{}{},
		"defaultInputModes":  []string{"text"},
		"defaultOutputModes": []string{"text"},
		"protocolVersions":   []string{"1.0"},
	})
	resp, _ = http.Post(kubemqURL+"/agents/register", "application/json", bytes.NewReader(card))
	resp.Body.Close()
	fmt.Printf("Re-registered: %d\n", resp.StatusCode)

	fmt.Println("\n=== Deregister via DELETE ===")
	req, _ := http.NewRequest(http.MethodDelete, kubemqURL+"/agents/"+agentID, nil)
	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "DELETE failed: %v\n", err)
		os.Exit(1)
	}
	resp.Body.Close()
	fmt.Printf("DELETE /agents/%s: %d\n", agentID, resp.StatusCode)

	resp, _ = http.Get(kubemqURL + "/agents/" + agentID)
	resp.Body.Close()
	fmt.Printf("GET /agents/%s after delete: %d\n", agentID, resp.StatusCode)

	fmt.Println("\nBoth deregistration methods demonstrated successfully!")
}
