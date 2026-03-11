import { Link } from "react-router-dom";

const navLinks = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Scenario Lab", to: "/scenario" },
  { label: "Reports", to: "/reports" },
  { label: "Docs", href: "#" },
  { label: "GitHub", href: "#" },
] as const;

export function LandingFooter() {
  return (
    <footer className="border-t border-[#24314F]">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
          {/* Brand & tagline */}
          <div className="max-w-sm">
            <p className="text-sm font-bold">InvestorFrame</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Event-driven market intelligence for macro signals, sector
              rotation, and watchlist analysis.
            </p>
          </div>

          {/* Nav links */}
          <nav className="flex flex-wrap items-center gap-6">
            {navLinks.map((link) =>
              "to" in link ? (
                <Link
                  key={link.label}
                  to={link.to}
                  className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link.label}
                </Link>
              ) : (
                <a
                  key={link.label}
                  href={link.href}
                  className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link.label}
                </a>
              ),
            )}
          </nav>
        </div>

        {/* Disclaimer & copyright */}
        <div className="mt-10 space-y-2">
          <p className="text-xs text-[#7F8BA7]">
            For research, education, and experimentation only. Not investment
            advice.
          </p>
          <p className="text-xs text-[#7F8BA7]">
            &copy; 2026 InvestorFrame. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
