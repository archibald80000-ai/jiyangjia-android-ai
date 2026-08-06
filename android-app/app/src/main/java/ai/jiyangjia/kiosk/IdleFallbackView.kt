package ai.jiyangjia.kiosk

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.view.View
import android.view.animation.LinearInterpolator
import kotlin.math.sin

class IdleFallbackView(context: Context) : View(context) {
    private val backgroundPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(20, 32, 36) }
    private val floorPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(30, 52, 55) }
    private val figurePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(232, 237, 226) }
    private val accentPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(66, 145, 136) }
    private val softPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.argb(70, 255, 255, 255) }
    private var phase = 0f

    private val animator = ValueAnimator.ofFloat(0f, 1f).apply {
        duration = 3600L
        repeatCount = ValueAnimator.INFINITE
        interpolator = LinearInterpolator()
        addUpdateListener {
            phase = it.animatedFraction
            invalidate()
        }
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        animator.start()
    }

    override fun onDetachedFromWindow() {
        animator.cancel()
        super.onDetachedFromWindow()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val w = width.toFloat()
        val h = height.toFloat()
        canvas.drawRect(0f, 0f, w, h, backgroundPaint)
        canvas.drawOval(RectF(-w * 0.2f, h * 0.68f, w * 1.2f, h * 1.12f), floorPaint)

        val breath = sin(phase * Math.PI * 2).toFloat()
        val cx = w * 0.5f
        val headY = h * 0.28f + breath * 5f
        val bodyTop = h * 0.42f + breath * 4f

        canvas.drawCircle(cx, headY, h * 0.085f, figurePaint)
        canvas.drawRoundRect(
            RectF(cx - w * 0.09f, bodyTop, cx + w * 0.09f, h * 0.66f),
            36f,
            36f,
            figurePaint
        )
        canvas.drawRoundRect(
            RectF(cx - w * 0.13f, h * 0.5f, cx + w * 0.13f, h * 0.56f),
            28f,
            28f,
            accentPaint
        )
        canvas.drawCircle(cx - w * 0.22f, h * 0.38f, 10f + breath * 2f, softPaint)
        canvas.drawCircle(cx + w * 0.24f, h * 0.31f, 8f - breath * 2f, softPaint)
    }
}
