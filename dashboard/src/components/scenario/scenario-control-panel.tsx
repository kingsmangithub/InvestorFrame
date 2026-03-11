"use client";

import { useState } from "react";
import { Play, RotateCcw, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SCENARIO_TEMPLATES, SCENARIO_CATEGORIES } from "@/lib/constants";

interface ScenarioControlPanelProps {
  selectedScenario: string;
  onSelect: (name: string) => void;
  onRun: () => void;
  onReset: () => void;
  isRunning: boolean;
}

export function ScenarioControlPanel({
  selectedScenario,
  onSelect,
  onRun,
  onReset,
  isRunning,
}: ScenarioControlPanelProps) {
  const [activeCategory, setActiveCategory] = useState<string>("All");

  const filteredTemplates =
    activeCategory === "All"
      ? SCENARIO_TEMPLATES
      : SCENARIO_TEMPLATES.filter((t) => t.category === activeCategory);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Scenario Controls</CardTitle>
        <CardDescription>
          Select a scenario to stress-test the current market frame.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Category filter tabs */}
        <div className="flex flex-wrap gap-1.5">
          {SCENARIO_CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={cn(
                "rounded-md px-3 py-1 text-xs font-medium transition-colors",
                activeCategory === cat
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-muted-foreground hover:text-foreground",
              )}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Template grid */}
        <div className="grid gap-2 sm:grid-cols-2">
          {filteredTemplates.map((template) => (
            <button
              key={template.name}
              onClick={() => onSelect(template.name)}
              disabled={isRunning}
              className={cn(
                "rounded-lg border p-3 text-left transition-colors",
                selectedScenario === template.name
                  ? "border-primary bg-primary/5"
                  : "border-border bg-transparent hover:bg-muted/50",
                isRunning && "opacity-50 cursor-not-allowed",
              )}
            >
              <p className="text-sm font-medium text-foreground">
                {template.label}
              </p>
              <p className="mt-0.5 text-xs text-muted-foreground line-clamp-2">
                {template.description}
              </p>
            </button>
          ))}
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2 pt-2">
          <Button
            onClick={onRun}
            disabled={!selectedScenario || isRunning}
            size="sm"
          >
            {isRunning ? (
              <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
            ) : (
              <Play className="mr-1.5 h-3.5 w-3.5" />
            )}
            {isRunning ? "Running..." : "Run Scenario"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={onReset}
            disabled={isRunning}
          >
            <RotateCcw className="mr-1.5 h-3.5 w-3.5" />
            Reset
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
