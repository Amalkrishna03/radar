"use client"

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
const chartData = [
  { date: "2024-04-01", car: 222, person: 150 },
  { date: "2024-04-02", car: 97, person: 180 },
  { date: "2024-04-03", car: 167, person: 120 },
  { date: "2024-04-04", car: 242, person: 260 },
  { date: "2024-04-05", car: 373, person: 290 },
  { date: "2024-04-06", car: 301, person: 340 },
  { date: "2024-04-07", car: 245, person: 180 },
  { date: "2024-04-08", car: 409, person: 320 },
  { date: "2024-04-09", car: 59, person: 110 },
]

const chartConfig = {
  anomalies: {
    label: "Anomalies",
  },
  // car: {
  //   label: "Car",
  //   color: "hsl(var(--chart-4))",
  // },
  person: {
    label: "Person",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig

function EventGraph({ events }: { events: object }) {
  return (
    <>
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
        <div className="grid flex-1 gap-1 text-center sm:text-left">
          <CardTitle>Showing total anomalies</CardTitle>
          <CardDescription>
            Area Chart
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="fillCar" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-car)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-car)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillPerson" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-person)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-person)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => {
                const date = new Date(value)
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })
              }}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(value) => {
                    return new Date(value).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    })
                  }}
                  indicator="dot"
                />
              }
            />
            <Area
              dataKey="person"
              type="natural"
              fill="url(#fillPerson)"
              stroke="var(--color-person)"
              stackId="a"
            />
            <Area
              dataKey="car"
              type="natural"
              fill="url(#fillCar)"
              stroke="var(--color-car)"
              stackId="a"
            />
            <ChartLegend content={<ChartLegendContent />} />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </>
  )
}

export default EventGraph