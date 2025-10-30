'use client'

import { useCallback, useState } from 'react'
import { Upload, X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface UploadBoxProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
  onClear: () => void
}

export default function UploadBox({ onFileSelect, selectedFile, onClear }: UploadBoxProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      e.stopPropagation()
      setIsDragging(false)

      const files = e.dataTransfer.files
      if (files && files.length > 0) {
        handleFile(files[0])
      }
    },
    [onFileSelect]
  )

  const handleFile = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file)

      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleClear = () => {
    setPreview(null)
    onClear()
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!preview ? (
        <div
          className={cn(
            'relative border-2 border-dashed rounded-lg p-12 text-center transition-colors',
            isDragging
              ? 'border-primary bg-primary/5'
              : 'border-gray-300 hover:border-primary/50'
          )}
          onDragEnter={handleDragIn}
          onDragLeave={handleDragOut}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept="image/*"
            onChange={handleFileInput}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <div className="flex flex-col items-center gap-4">
            <div className="p-4 bg-primary/10 rounded-full">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-700">
                Drop your food photo here
              </p>
              <p className="text-sm text-gray-500 mt-1">or click to browse</p>
            </div>
            <p className="text-xs text-gray-400">Supports: JPG, PNG, WebP</p>
          </div>
        </div>
      ) : (
        <div className="relative rounded-lg overflow-hidden border-2 border-gray-200">
          <img src={preview} alt="Preview" className="w-full h-auto max-h-96 object-contain" />
          <button
            onClick={handleClear}
            className="absolute top-2 right-2 p-2 bg-white rounded-full shadow-lg hover:bg-gray-100 transition-colors"
            aria-label="Clear image"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      )}
    </div>
  )
}
