import { useEffect, useState } from "react";
import type { DashboardData } from "./types/dashboard";
import { Header } from "./components/Header";
import { VulnerabilityScore } from "./components/VulnerabilityScore";
import { PollutantCard } from "./components/PollutantCard";
import { RoomStatus } from "./components/RoomStatus";

export default function App() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard")
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return <div className="p-10">Chargement...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-10 space-y-8">
      
      <Header
        patient={data.selected_patient_id}
        status={data.risk_category}
        lastUpdate={data.last_update}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <div className="lg:col-span-2">
          <VulnerabilityScore
            score={{
              value: data.risk_score,
              level: data.risk_category,
              actions: data.actions
            }}
          />
        </div>

        <RoomStatus status={data.risk_category} />

      </div>

      {/* GRID POLLUANTS CORRIGÉ */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(data.pollutants).map(([name, pollutant]) => (
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