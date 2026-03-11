import { Clock, User, ArrowLeft } from 'lucide-react';
import type { RiskLevel } from "../types/dashboard";
import { Link } from 'react-router';


interface HeaderProps {
  room_id: number;
  nb_patient: number;
  status: RiskLevel;
  lastUpdate: string;
}

export function Header({ nb_patient, status, lastUpdate, room_id }: HeaderProps) {

  const getStatusColor = () => {
    switch (status) {
      case 'OPTIMAL':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'MODÉRÉ':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'ÉLEVÉ':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'CRITIQUE':
        return 'bg-red-100 text-red-800 border-red-200';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'OPTIMAL':
        return '🟢';
      case 'MODÉRÉ':
        return '🟡';
      case 'ÉLEVÉ':
        return '🟠';
      case 'CRITIQUE':
        return '🔴';
    }
  };

  return (
    <header className="bg-white rounded-xl shadow-sm p-6">
      <Link 
        to="/"
        className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="text-sm font-medium">Retour à la supervision</span>
      </Link>

      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">Chambre {room_id}</h1>
          <div className="flex items-center gap-2 text-gray-600 mb-1">
            <User className="w-4 h-4" />
            <span className="font-medium">{nb_patient} patient(s) détecté(s)</span>
          </div>
        </div>
      

              <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Clock className="w-4 h-4" />
            <span>Dernière mise à jour : {lastUpdate}</span>
          </div>
          
          <div className={`px-4 py-2 rounded-lg border-2 font-medium flex items-center gap-2 ${getStatusColor()}`}>
            <span className="text-lg">{getStatusIcon()}</span>
            {status}
          </div>
        </div>
      </div>
    </header>
  );
}