import { IonCard, IonCardContent, IonCardTitle } from "@ionic/react"
import { useEffect, useRef, useState } from "react"
import { CurrencyCode, CurrencyListItem, useCurrencyListStore } from "../stores/CurrencyList"
import { useShallow } from "zustand/shallow"
import { CurrencyHistory, useCurrencyHistoryStore } from "../stores/CurrencyHistory"
import { useNMonthsStore } from "../stores/nMonthsStore"


type TooltipHit = { x: number; y: number; text: string }

// for now
const tooltipHits: TooltipHit[] = []
const tooltipWidth = 200

const CurrencyRatesCanvasCard: React.FC = () => {
  // stores
  const [selectedCurrencies, currencyList] = useCurrencyListStore(useShallow(s => [s.selected, s.list]))
  const [currencyHistory] = useCurrencyHistoryStore(useShallow(s => [s.history]))
  const [nMonthsToView] = useNMonthsStore(useShallow(s => [s.nMonthsToView]))

  const canvasRef = useRef<HTMLCanvasElement | null>(null)  // html canvas reference
  const wrapperRef = useRef<HTMLDivElement | null>(null) // wrapper around canvas
  const [tooltip, setTooltip] = useState<TooltipHit | null>(null)

  // rendering effect when selected currencies change or currency history changes
  useEffect(() => {
    const canvas = canvasRef.current
    const wrapper = wrapperRef.current
    if (!canvas || !wrapper) return

    const resizeObserver = new ResizeObserver(() => {
      canvas.width = wrapper.clientWidth
      canvas.height = 500
      renderCurrencyChart(canvasRef.current!, currencyList, selectedCurrencies, currencyHistory, nMonthsToView)
    })

    resizeObserver.observe(wrapper)

    return () => {
      resizeObserver.disconnect()
    }
  }, [selectedCurrencies, currencyHistory, nMonthsToView])

  // handle showing tooltip when mouse hovers
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      const x = e.clientX - rect.x
      const y = e.clientY - rect.y

      const hit = findTooltipAt(x, y)
      setTooltip(hit)
    }

    canvas.addEventListener("mousemove", handleMouseMove)

    return () => {
      canvas.removeEventListener("mousemove", handleMouseMove)
    }
  }, [selectedCurrencies, currencyHistory, nMonthsToView])


  useEffect(() => {
    if (!tooltip) return
    const canvas = canvasRef.current
    canvas?.getContext("2d") 
  }, [tooltip])

  return (
    <IonCard >
      <IonCardTitle>
      </IonCardTitle>
      <IonCardContent>
        <div ref={wrapperRef} style={{ width: "100%", position: "relative" }}>
          <canvas
            ref={canvasRef}
            style={{
              width: "100%",
              border: "1px solid black",
              borderRadius: 4,
            }}
          >
          </canvas>
          {tooltip && (
            <div
              style={{
                position: "absolute",
                left: (() => {
                  const canvasWidth = canvasRef.current?.width ?? 100
                  if (tooltip.x + tooltipWidth >= canvasWidth) {// over the limit
                    return canvasWidth - tooltipWidth 
                  }
                  return tooltip.x + 10
                })(),
                top: tooltip.y,
                background: "rgba(0,0,0,0.7)",
                color: "white",
                padding: "4px 6px",
                borderRadius: 4,
                fontSize: 18,
                pointerEvents: "none",
              }}
            >
              {tooltip.text}
            </div>
          )}
        </div>
      </IonCardContent>
    </IonCard>
  )
}

export default CurrencyRatesCanvasCard




// aproximate area
function findTooltipAt(x: number, y: number): TooltipHit | null {
  const errorMargin = 12

  for (const hit of tooltipHits) {
    const dx = x - hit.x
    // const dy = y - hit.y
    const error = dx * dx // + dy * dy
    if (Math.sqrt(error) < errorMargin)
      return { ...hit }  // copy
  }
  return null
}



function renderCurrencyChart(
  canvas: HTMLCanvasElement,
  currencyList: CurrencyListItem[],
  selectedCurrencies: string[],
  currencyHistory: CurrencyHistory,
  monthCount: number
) {
  // get context, w, h
  const context = canvas.getContext("2d")
  if (!context) return

  const width = canvas.width
  const height = canvas.height

  context.clearRect(0, 0, width, height) // clear canvas

  tooltipHits.splice(0, tooltipHits.length) // clear tooltip hits

  const currencyEntries = currencyHistory.entries().toArray() // calculate length of one entry in history
  if (currencyEntries.length == 0) {
    console.warn("No entries in currency history.")
    return
  }

  const currencyEntryCount = Array.from(currencyEntries[0][1].keys()).length // actual length
  const effectiveLength = Math.min(currencyEntryCount, monthCount) // this is the effective length

  drawVericalLines(context, width, height, effectiveLength - 1) // draws a vertical lines
  const [lowestRate, highestRate] = GetSelectedCurrencyLimits(currencyHistory, selectedCurrencies, effectiveLength) // get limits

  // render out rates or every selected currency
  for (const currency of selectedCurrencies) {
    const currencyRates = currencyHistory.get(currency)  // get rates of a specific currency
    if (currencyRates === undefined) {  // if rates are not present, skip
      console.warn("Currency isn't loaded in the history, there's nothing to render!")
      continue
    }

    const sortedEntries = Array.from(currencyRates).sort((a, b) => new Date(a[0]).getTime() - new Date(b[0]).getTime())
    const entries = sortedEntries.slice(-effectiveLength) // get effective length of the most recent chunk

    const firstCurrency = Array.from(currencyHistory.values())[0]
    let dates = Array.from(firstCurrency.keys()).sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
    dates = dates.slice(-effectiveLength)

    drawXAxisNumbers(context, dates, width, height, highestRate, lowestRate, effectiveLength)
    drawYAxisNumbers(context, width, height, highestRate, lowestRate)
    drawTrendLine(context, currencyList, dates, currency, entries, width, height, highestRate, lowestRate)
    drawAreaUnderneath(context, entries, width, height, highestRate, lowestRate)
  }
}

function drawTrendLine(
  context: CanvasRenderingContext2D,
  currencyList: CurrencyListItem[],
  dates: string[],
  currency: string,
  entries: [string, number][],
  width: number, height: number,
  highestRate: number, lowestRate: number
) {
  const effectiveLength = entries.length

  context.beginPath()
  context.lineWidth = 3

  const baseRadius = 10;
  const radius = baseRadius / Math.sqrt(effectiveLength);

  for (let i = 0; i < effectiveLength - 1; i++) {
    const x1 = i / (effectiveLength - 1) * width
    const x2 = (i + 1) / (effectiveLength - 1) * width

    let y1 = getPercentageInRange(entries[i][1], highestRate, lowestRate)
    let y2 = getPercentageInRange(entries[i + 1][1], highestRate, lowestRate)

    const scale = 0.8
    y1 = (y1 - 0.5) * scale + 0.5
    y2 = (y2 - 0.5) * scale + 0.5
    y1 *= height
    y2 *= height

    // store tooltip hit
    tooltipHits.push({ x: x1, y: y1, text: 
`${currency}: 
${entries[i][1]} ${currencyList.find(x => x.code == currency)?.currencyLabel} 
(${entries[i][0]})` 
    })

    const goingUp = entries[i + 1][1] >= entries[i][1]
    context.strokeStyle = goingUp ?  "#28a745" : "#dc3545"

    context.beginPath()
    context.moveTo(x1, y1)
    context.lineTo(x2, y2)
    context.stroke()

    // draw circle
    context.beginPath()
    context.arc(x1, y1, radius, 0, 2 * Math.PI, false)
    context.fillStyle = "#343a40"
    context.fill()
    context.lineWidth = 5
    context.strokeStyle = "#343a40"
    context.stroke()
    context.arc
  }


  context.stroke()
}

function drawYAxisNumbers(context: CanvasRenderingContext2D, width: number, height: number, highestRate: number, lowestRate: number) {
  const steps = 10
  context.fillStyle = "black"
  context.font = "14px"
  // context.textAlign = "right"
  // context.textBaseline = "middle"

  const paddingLeft = 10

  for (let i = 0; i <= steps; i++) {
    const t = i / steps
    const value = highestRate - t * (highestRate - lowestRate)
    const y = t * height

    context.fillText(value.toFixed(2), paddingLeft - 8, y - 8)
    
    // Optional horizontal guide line
    context.strokeStyle = "rgba(0, 0, 0, 0.1)"
    context.beginPath()
    context.moveTo(paddingLeft, y)
    context.lineTo(width, y)
    context.stroke()
  }
}

function drawXAxisNumbers(
  context: CanvasRenderingContext2D, 
  dates: string[], 
  width: number, 
  height: number, 
  highestRate: number,
  lowestRate: number, 
  count: number
) {
  const stepWidth = 100
  const steps = Math.floor(width / stepWidth)
  context.fillStyle = "black"
  context.font = "14px"
  // context.textAlign = "right"
  // context.textBaseline = "middle"

  const y = 0.03 * height 

  const indexScaler = dates.length / steps
  
  for (let i = 0; i <= steps; i++) {
    const stepSize = width / steps
    const x = i * stepSize + 0.15 * stepSize 

    const dateIndex = Math.floor(i * indexScaler)
    const date = dates[dateIndex]

    const text =  `${date}`

    context.fillText(text, x, y)
  }
}


function drawAreaUnderneath(
  context: CanvasRenderingContext2D,
  entries: [string, number][],
  width: number, height: number,
  highestRate: number, lowestRate: number
): void {
  const effectiveLength = entries.length

  // draws the same line, without styling
  const path = new Path2D()
  path.moveTo(0, height)

  for (let i = 0; i < effectiveLength; i++) {
    const x = i / (effectiveLength - 1) * width
    let y = getPercentageInRange(entries[i][1], highestRate, lowestRate)
    const scale = 0.8
    y = (y - 0.5) * scale + 0.5
    y *= height

    if (i === 0) {
      path.lineTo(x, y)
    } else {
      path.lineTo(x, y)
    }
  }

  path.lineTo(width, height)
  path.closePath()

  // gradient
  const fillGradient = context.createLinearGradient(0, 0, 0, height)
  fillGradient.addColorStop(0, "rgba(0, 255, 0, 0.15)") // green
  fillGradient.addColorStop(1, "rgba(0, 255, 0, 0)")    // transparent

  context.fillStyle = fillGradient
  context.fill(path) // fill area underneath
}


function getPercentageInRange(value: number, low: number, high: number): number {
  return (value - low) / (high - low)
}


function drawVericalLines(
  context: CanvasRenderingContext2D,
  width: number,
  height: number,
  monthCount: number
) {
  if (monthCount <= 0) {
    console.warn("No entries in currency history.")
    return
  }

  context.strokeStyle = "lightgray"

  for (let i = 0; i < monthCount; i++) {
    const x = i / monthCount * width
    context.beginPath()
    context.moveTo(x, 0)
    context.lineTo(x, height)
    context.stroke()
  }
}


function GetSelectedCurrencyLimits(
  currencyHistory: CurrencyHistory,
  selectedCurrencies: CurrencyCode[],
  monthCount: number
): [number, number] {
  let minRate = Number.POSITIVE_INFINITY
  let maxRate = Number.NEGATIVE_INFINITY

  for (const currency of selectedCurrencies) {
    const currencyRates = currencyHistory.get(currency)
    if (!currencyRates) {
      console.warn("Currency isn't loaded in the history, can't be assessed for limit rates!")
      continue
    }

    const entries = Array.from(currencyRates).sort((a, b) => new Date(a[0]).getTime() - new Date(b[0]).getTime())

    if (entries.length < monthCount) {
      console.warn("Month count must be less than length of entries.")
      continue
    }

    const recent = entries.slice(-monthCount)

    minRate = Math.min(Math.min(...recent.map(x => x[1])), minRate)
    maxRate = Math.max(Math.max(...recent.map(x => x[1])), maxRate)
  }

  return [minRate, maxRate]
}

