import { AlertCircle } from "lucide-react";

interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-5">
      <div className="flex items-start gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-rose-400" />
        <div>
          <p className="text-sm font-medium text-rose-300">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 rounded-lg border border-rose-500/30 px-3 py-1.5 text-sm text-rose-300 transition hover:border-rose-500/50 hover:text-rose-200"
            >
              Retry
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
