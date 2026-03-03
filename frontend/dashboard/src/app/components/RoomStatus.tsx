import type { RiskLevel } from "../types/dashboard";

interface RoomStatusProps {
  status: RiskLevel;
}

export function RoomStatus({ status }: RoomStatusProps) {

  const getStatusConfig = () => {
    switch (status) {
      case 'OPTIMAL':
        return {
          color: 'bg-green-500',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          textColor: 'text-green-900',
          label: 'OPTIMAL',
          description: 'Conditions optimales – Aucune action requise.'
        };

      case 'MODÉRÉ':
        return {
          color: 'bg-yellow-500',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          textColor: 'text-yellow-900',
          label: 'VIGILANCE',
          description: 'Surveillance recommandée – Ajustement automatique actif.'
        };

      case 'ÉLEVÉ':
        return {
          color: 'bg-orange-500',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
          textColor: 'text-orange-900',
          label: 'DANGER',
          description: 'Attention – Intervention recommandée.'
        };

      case 'CRITIQUE':
        return {
          color: 'bg-red-500',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          textColor: 'text-red-900',
          label: 'URGENCE',
          description: "Action immédiate requise – Protocole d'urgence."
        };

      default:
        return {
          color: 'bg-gray-400',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
          textColor: 'text-gray-700',
          label: 'INCONNU',
          description: 'Statut indisponible.'
        };
    }
  };

  const config = getStatusConfig();

  return (
    <div className={`bg-white rounded-xl shadow-sm p-8 border-2 ${config.borderColor} ${config.bgColor} h-full flex flex-col items-center justify-center`}>

      <h2 className="text-lg font-semibold text-gray-900 mb-6">
        État global de la chambre
      </h2>

      <div className={`w-32 h-32 rounded-full ${config.color} shadow-lg mb-6 flex items-center justify-center relative`}>
        <div className="w-24 h-24 rounded-full bg-white/30 animate-pulse"></div>
        <div className="absolute inset-0 rounded-full border-4 border-white/50"></div>
      </div>

      <div className={`text-3xl font-bold ${config.textColor} tracking-wide mb-3`}>
        {config.label}
      </div>

      <p className={`text-sm ${config.textColor} text-center max-w-xs`}>
        {config.description}
      </p>

    </div>
  );
}