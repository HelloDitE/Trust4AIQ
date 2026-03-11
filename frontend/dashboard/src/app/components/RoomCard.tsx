import type { RiskLevel } from "../types/dashboard";
import { Users, ArrowRight } from 'lucide-react';
import { Link } from 'react-router';

interface RoomCardProps {
  id: string;
  name: string;
  patientCount: number;
  globalScore: number;
  riskCategory: RiskLevel;
}

export function RoomCard({id, patientCount, globalScore, riskCategory }: RoomCardProps) {
  const getCardStyle = () => {
    switch (riskCategory) {
      case 'OPTIMAL':
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          badge: 'bg-green-100 text-green-800 border-green-200',
          score: 'text-green-600'
        };
      case 'MODÉRÉ':
        return {
          bg: 'bg-yellow-50',
          border: 'border-yellow-200',
          badge: 'bg-yellow-100 text-yellow-800 border-yellow-200',
          score: 'text-yellow-600'
        };
      case 'ÉLEVÉ':
        return {
          bg: 'bg-orange-50',
          border: 'border-orange-200',
          badge: 'bg-orange-100 text-orange-800 border-orange-200',
          score: 'text-orange-600'
        };
      case 'CRITIQUE':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          badge: 'bg-red-100 text-red-800 border-red-200',
          score: 'text-red-600'
        };
    }
  };

  const style = getCardStyle();

  return (
    <div className={`${style.bg} border-2 ${style.border} rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-900">Chambre {id}</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-medium border ${style.badge}`}>
          {riskCategory}
        </span>
      </div>

      <div className="flex items-center gap-2 text-gray-600 mb-4">
        <Users className="w-4 h-4" />
        <span className="text-sm">{patientCount} patient{patientCount > 1 ? 's' : ''} détecté{patientCount > 1 ? 's' : ''}</span>
      </div>

      <div className="mb-6">
        <div className="flex items-baseline gap-2 mb-2">
          <span className="text-sm text-gray-600">SVP :</span>
          <span className={`text-4xl font-bold ${style.score}`}>{globalScore.toFixed(2)}</span>
        </div>
      </div>

      <Link 
        to={`/rooms/${id}`}
        className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-white border-2 border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 hover:border-gray-400 transition-colors"
      >
        Voir le détail
        <ArrowRight className="w-4 h-4" />
      </Link>
    </div>
  );
}
