import React from 'react'

type Variant = 'error' | 'warning' | 'info' | 'success'

type Props = {
  message: string
  variant?: Variant
  onClose?: () => void
  onRetry?: () => void
}

const styles: Record<Variant, string> = {
  error: 'bg-red-600 text-white',
  warning: 'bg-yellow-500 text-black',
  info: 'bg-blue-600 text-white',
  success: 'bg-green-600 text-white'
}

export default function ErrorBanner({
  message,
  variant = 'error',
  onClose,
  onRetry
}: Props) {
  if (!message) return null

  return (
    <div
      className={`w-full px-4 py-3 mb-4 rounded flex items-center justify-between ${styles[variant]}`}
    >
      <div className="flex items-center gap-3">
        {/* Icon */}
        <span className="text-lg">
          {variant === 'error' && '❌'}
          {variant === 'warning' && '⚠️'}
          {variant === 'info' && 'ℹ️'}
          {variant === 'success' && '✅'}
        </span>

        {/* Message */}
        <span className="text-sm font-medium">{message}</span>
      </div>

      <div className="flex items-center gap-2">
        {/* Retry Button */}
        {onRetry && (
          <button
            onClick={onRetry}
            className="bg-white/20 px-3 py-1 rounded text-sm hover:bg-white/30"
          >
            Retry
          </button>
        )}

        {/* Close Button */}
        {onClose && (
          <button
            onClick={onClose}
            className="bg-black/20 px-2 py-1 rounded hover:bg-black/30"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}