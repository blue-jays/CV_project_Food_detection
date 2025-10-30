'use client'

import { Loader2 } from 'lucide-react'

interface LoadingOverlayProps {
  message?: string
}

export default function LoadingOverlay({ message = 'Processing...' }: LoadingOverlayProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 flex flex-col items-center gap-4 shadow-2xl">
        <Loader2 className="w-12 h-12 text-primary animate-spin" />
        <p className="text-lg font-medium text-gray-700">{message}</p>
      </div>
    </div>
  )
}
