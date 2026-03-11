export function FooterStatus() {
  return (
    <footer className="border-t py-3 px-6">
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
            API Connected
          </span>
          <span>Source: Demo Data</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Last updated: just now</span>
          <span>v0.1.0</span>
        </div>
      </div>
    </footer>
  );
}
