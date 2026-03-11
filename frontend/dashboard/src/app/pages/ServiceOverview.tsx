import { useEffect, useState } from "react";
import { Clock, Activity, AlertCircle } from 'lucide-react';
import {RoomCard} from '../components/RoomCard';
import type { JSX } from "react/jsx-runtime";
import type { RiskLevel } from "../types/dashboard";


interface Room {
  risk_score: number;
  room_id: string;
  patients_count: number;
  risk_category: RiskLevel;
}

interface Stats {
  totalRooms: number;
  roomsOptimal: number;
  roomsInVigilance: number;
  roomsInDanger: number;
}

interface RoomsResponse {
  map(arg0: (data: any) => JSX.Element): import("react").ReactNode;
  rooms: Room[];
  stats: Stats;
}


export function ServiceOverview() {
  const [data, setData] = useState<RoomsResponse | null>(null);
  const currentTime = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  const currentDate = new Date().toLocaleDateString('fr-FR', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  useEffect(() => { 
    fetch(`http://127.0.0.1:8000/rooms`)
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  });

  if (!data) {
    return <div className="p-10">Chargement...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-8">
        {/* Header */}
        <header className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-3xl font-semibold text-gray-900 mb-2">
                Supervision – Service de Réanimation
              </h1>
              <p className="text-gray-600 capitalize">{currentDate}</p>
            </div>
            
            <div className="flex items-center gap-2 text-gray-600 bg-gray-50 px-4 py-2 rounded-lg">
              <Clock className="w-5 h-5" />
              <span className="font-medium">Mise à jour : {currentTime}</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-blue-600" />
                <span className="text-sm text-gray-600">Chambres surveillées</span>
              </div>
              <p className="text-3xl font-bold text-gray-900">{data.stats.totalRooms}</p>
            </div>

            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm text-gray-600">Optimal</span>
              </div>
              <p className="text-3xl font-bold text-green-600">{data.stats.roomsOptimal}</p>
            </div>

            <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm text-gray-600">Vigilance</span>
              </div>
              <p className="text-3xl font-bold text-yellow-600">{data.stats.roomsInVigilance}</p>
            </div>

            <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-5 h-5 text-orange-600" />
                <span className="text-sm text-gray-600">Danger/Urgence</span>
              </div>
              <p className="text-3xl font-bold text-orange-600">{data.stats.roomsInDanger}</p>
            </div>
          </div>

          {data.stats.roomsInVigilance > 0 && (
            <div className="mt-4 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">
              <p className="text-sm text-yellow-800">
                <span className="font-semibold">Indicateur global :</span> {data.stats.roomsInVigilance} chambre{data.stats.roomsInVigilance > 1 ? 's' : ''} en vigilance
              </p>
            </div>
          )}

          {data.stats.roomsInDanger > 0 && (
            <div className="mt-4 p-3 bg-orange-50 border-l-4 border-orange-500 rounded">
              <p className="text-sm text-orange-800">
                <span className="font-semibold">⚠️ Alerte :</span> {data.stats.roomsInDanger} chambre{data.stats.roomsInDanger > 1 ? 's' : ''} en danger nécessitant une attention immédiate
              </p>
            </div>
          )}
        </header>

        {/* Room Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.rooms.map((room) => (
            <RoomCard
              id={room.room_id}
              patientCount={room.patients_count}
              riskCategory={room.risk_category}
              globalScore={room.risk_score} name={""}            
              />
          ))}
        </div>
      </div>
    </div>
  );
}
