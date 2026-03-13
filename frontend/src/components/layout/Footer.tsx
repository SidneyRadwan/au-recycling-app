import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t bg-muted mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="flex items-center gap-2 font-bold text-green-700 dark:text-green-400">
            <span aria-hidden="true">♻️</span>
            <span>Australia Recycling</span>
          </div>

          <p className="text-sm text-muted-foreground max-w-md">
            This site is free to use. Small ads help cover our hosting and AI costs.
          </p>

          <nav className="flex items-center gap-4 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-green-700 transition-colors">
              Home
            </Link>
            <span aria-hidden="true">|</span>
            <Link href="/councils" className="hover:text-green-700 transition-colors">
              Councils
            </Link>
            <span aria-hidden="true">|</span>
            <Link href="/materials" className="hover:text-green-700 transition-colors">
              Materials
            </Link>
            <span aria-hidden="true">|</span>
            <Link href="/privacy" className="hover:text-green-700 transition-colors">
              Privacy
            </Link>
            <span aria-hidden="true">|</span>
            <Link href="/about" className="hover:text-green-700 transition-colors">
              About
            </Link>
          </nav>

          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} Australia Recycling. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
