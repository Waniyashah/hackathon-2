import './globals.css'
import { AuthProvider } from '../components/AuthProvider'

export const metadata = {
  title: 'Todo App',
  description: 'A simple todo application with authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}