package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "full-info-agent-01"
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

	var data map[string]interface{}
	json.Unmarshal(body, &data)

	fmt.Println("\n--- Agent Card ---")
	fmt.Printf("  agent_id:           %v\n", data["agent_id"])
	fmt.Printf("  name:               %v\n", data["name"])
	fmt.Printf("  description:        %v\n", data["description"])
	fmt.Printf("  version:            %v\n", data["version"])
	fmt.Printf("  url:                %v\n", data["url"])
	fmt.Printf("  defaultInputModes:  %v\n", data["defaultInputModes"])
	fmt.Printf("  defaultOutputModes: %v\n", data["defaultOutputModes"])
	fmt.Printf("  protocolVersions:   %v\n", data["protocolVersions"])
	fmt.Printf("  registered_at:      %v\n", data["registered_at"])
	fmt.Printf("  last_seen:          %v\n", data["last_seen"])

	skills, _ := data["skills"].([]interface{})
	fmt.Printf("\n--- Skills (%d) ---\n", len(skills))
	for _, s := range skills {
		sk, _ := s.(map[string]interface{})
		fmt.Printf("  [%v] %v: %v\n", sk["id"], sk["name"], sk["description"])
		fmt.Printf("    tags: %v\n", sk["tags"])
	}
}
