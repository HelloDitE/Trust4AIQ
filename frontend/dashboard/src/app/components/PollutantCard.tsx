import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import type { PollutantData } from "../types/dashboard";

interface PollutantProps {
  name: string;
  data: PollutantData;
}

export function PollutantCard({ name, data }: PollutantProps) {

  const getStatusConfig = () => {
    switch (data.status) {
      case 'BON':
        return {
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          textColor: 'text-green-700',
          badgeColor: 'bg-green-100 text-green-800',
          icon: <TrendingDown className="w-4 h-4" />
        };
      case 'MODERE':
        return {
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          textColor: 'text-yellow-700',
          badgeColor: 'bg-yellow-100 text-yellow-800',
          icon: <Minus className="w-4 h-4" />
        };
      case 'ELEVE':
        return {
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          textColor: 'text-red-700',
          badgeColor: 'bg-red-100 text-red-800',
          icon: <TrendingUp className="w-4 h-4" />
        };
      case 'CRITIQUE':
        return {
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          textColor: 'text-red-700',
          badgeColor: 'bg-red-100 text-red-800',
          icon: <TrendingUp className="w-4 h-4" />
        };
    }
  };

  const config = getStatusConfig();


  


return (
    <div className={`bg-white rounded-xl shadow-sm p-5 border ${config.borderColor} ${config.bgColor} transition-all hover:shadow-md`}>
      <div className="flex items-start justify-between mb-3">

        {/* Nom */}
        <h3 className="font-semibold text-gray-900">{name}</h3>
        <div className={`flex items-center gap-1 ${config.textColor}`}>
          {config.icon}
        </div>
      </div>

      <div className="mb-4">

        {/* Valeur */}
        <div className="flex items-baseline gap-1">
          <span className={`text-3xl font-bold ${config.textColor}`}>
            {data.value}
          </span>
          <span className="text-sm text-gray-500">{data.unit}</span>
        </div>
      </div>


      <div className="space-y-2">

        {/* Seuil */}
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Seuil recommandé</span>
          <span className="font-medium text-gray-900">
            {data.limit} {data.unit}
          </span>
        </div>


        {/* Badge */}
        <div className={`px-3 py-1 rounded-full text-sm font-medium text-center ${config.badgeColor}`}>
          {data.status}
        </div>
      </div>
    </div>
  );
}
