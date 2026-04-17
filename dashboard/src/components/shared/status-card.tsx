import { Card, CardContent } from "@/components/ui/card";

export function StatusCard({ message }: { message: string }) {
  return (
    <Card>
      <CardContent className="pt-5 text-sm text-muted-foreground">{message}</CardContent>
    </Card>
  );
}
