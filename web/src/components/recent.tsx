import * as React from "react"

import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import { useQuery } from "../hooks/fetcher"

export default function RecentComponents() {
  const { data, error, isLoading, isValidating, mutate } = useQuery(
    "/api/events/"
  );
  return (
    <Carousel>
      <CarouselContent>
        {Array.from({ length: 5 }).map((_, index) => (
          <CarouselItem key={index}>
            <Card className="rounded-2xl overflow-hidden">
              <img src="https://github.com/user-attachments/assets/42645a0c-adf7-4c21-8502-2b6979ca01a1" />
            </Card>
          </CarouselItem>
        ))}
      </CarouselContent>
      {/* <CarouselPrevious className="relative"/>
      <CarouselNext className="relative"/> */}
    </Carousel>
  )
}
