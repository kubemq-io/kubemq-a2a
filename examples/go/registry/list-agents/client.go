package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const kubemqURL = "http://localhost:9090"

func listAgents(url string, label string) {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	var agents []map[string]interface{}
	json.Unmarshal(body, &agents)

	fmt.Printf("=== %s ===\n", label)
	for _, agent := range agents {
		skills := []string{}
		if s, ok := agent["skills"].([]interface{}); ok {
			for _, sk := range s {
				if m, ok := sk.(map[string]interface{}); ok {
					skills = append(skills, fmt.Sprintf("%v", m["id"]))
				}
			}
		}
		fmt.Printf("  %s: skills=%v\n", agent["agent_id"], skills)
	}
	fmt.Printf("\nTotal: %d\n\n", len(agents))
}

func main() {
	listAgents(kubemqURL+"/agents", "All Agents")
	listAgents(kubemqURL+"/agents?skill_tags=echo", "Filter by skill_tags=echo")
	listAgents(kubemqURL+"/agents?skill_tags=nlp", "Filter by skill_tags=nlp")
}
