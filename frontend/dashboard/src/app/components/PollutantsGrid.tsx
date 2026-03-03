import { PollutantCard } from "./PollutantCard";
import type { PollutantData } from "../types/dashboard";


interface PollutantsGridProps {
  pollutants: Record<string, PollutantData>;
}

export function PollutantsGrid({ pollutants }: PollutantsGridProps) {
  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">
        Polluants mesurés
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
        {Object.entries(pollutants).map(([name, pollutant]) => (
          <PollutantCard
            key={name}
            name={name}
            data={pollutant}
          />
        ))}
      </div>
    </div>
  );
}



