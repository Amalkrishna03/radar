import * as React from "react"

import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

export default function RecentComponents({ data }: { data: any[] }) {
  if (!Array.isArray(data)) return null;

  return (
    <Carousel>
      <CarouselContent>
        {data.map((event, index) => (
          <CarouselItem key={index}>
            <Card className="rounded-2xl overflow-hidden">
              <img src={event.url} />
            </Card>
          </CarouselItem>
        ))}
      </CarouselContent>
      {/* <CarouselPrevious className="relative"/>
      <CarouselNext className="relative"/> */}
    </Carousel>
  )
}
