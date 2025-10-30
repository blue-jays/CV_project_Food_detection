'use client'

import { X, Trash2, History } from 'lucide-react'
import { HistoryItem } from '@/lib/history'

interface HistoryDrawerProps {
  isOpen: boolean
  onClose: () => void
  history: HistoryItem[]
  onSelectItem: (item: HistoryItem) => void
  onClearHistory: () => void
}

export default function HistoryDrawer({
  isOpen,
  onClose,
  history,
  onSelectItem,
  onClearHistory,
}: HistoryDrawerProps) {
  if (!isOpen) return null

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/30 z-40" onClick={onClose} />

      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-80 bg-white shadow-2xl z-50 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold">Recent Detections</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {history.length === 0 ? (
            <div className="text-center text-gray-500 mt-8">
              <History className="w-12 h-12 mx-auto mb-2 opacity-30" />
              <p>No history yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {history.map(item => (
                <button
                  key={item.id}
                  onClick={() => {
                    onSelectItem(item)
                    onClose()
                  }}
                  className="w-full text-left p-3 border rounded-lg hover:border-primary transition-colors"
                >
                  <img
                    src={item.imageUrl}
                    alt="History thumbnail"
                    className="w-full h-32 object-cover rounded mb-2"
                  />
                  <div className="text-xs text-gray-500 mb-1">
                    {new Date(item.timestamp).toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-700">
                    {item.ingredients.slice(0, 3).join(', ')}
                    {item.ingredients.length > 3 && ` +${item.ingredients.length - 3}`}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {history.length > 0 && (
          <div className="p-4 border-t">
            <button
              onClick={onClearHistory}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              Clear History
            </button>
          </div>
        )}
      </div>
    </>
  )
}
