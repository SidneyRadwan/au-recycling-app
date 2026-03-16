interface ErrorStateProps {
  message?: string
  className?: string
}

export function ErrorState({
  message = 'Please try again later.',
  className = 'py-20',
}: ErrorStateProps) {
  return (
    <div className={`text-center ${className}`}>
      <p className="text-lg font-medium text-foreground">Something went wrong</p>
      <p className="text-sm text-muted-foreground mt-1">{message}</p>
    </div>
  )
}
