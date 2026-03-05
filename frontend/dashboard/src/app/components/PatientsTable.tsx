import { AlertCircle } from 'lucide-react';

interface Patient {
  id: string;
  vuln_score: number;
  risk_score: number;
  risk_category: "OPTIMAL" | "MODÉRÉ" | "ÉLEVÉ" | "CRITIQUE";
}

interface PatientsTableProps {
  patients: Patient[];
  criticalPatient: string;
}

export function PatientsTable({ patients, criticalPatient }: PatientsTableProps) {
  const getLevelColor = (level: string) => {
    switch (level) {
      case 'OPTIMAL':
        return 'text-green-700 bg-green-100';
      case 'MODÉRÉ':
        return 'text-yellow-700 bg-yellow-100';
      case 'ÉLEVÉ':
        return 'text-orange-700 bg-orange-100';
      case 'CRITIQUE':
        return 'text-red-700 bg-red-100';
      default:
        return 'text-gray-700 bg-gray-100';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">
        Patients présents
      </h3>

      <div className="overflow-hidden rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Patient
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Score
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Niveau
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {patients.map((patient, index) => {
              const isCritical = patient.id === criticalPatient;
              return (
                <tr 
                  key={index}
                  className={isCritical ? 'bg-orange-50 border-l-4 border-orange-500' : ''}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900">{patient.id}</span>
                      {isCritical && (
                        <AlertCircle className="w-4 h-4 text-orange-600" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`font-semibold ${isCritical ? 'text-orange-700' : 'text-gray-900'}`}>
                      {patient.risk_score.toFixed(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getLevelColor(patient.risk_category)}`}>
                      {patient.risk_category}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-start gap-2 p-3 bg-orange-50 rounded-lg border border-orange-200">
        <AlertCircle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-orange-800">
          <span className="font-semibold">Score critique retenu pour le calcul global.</span>
          <br />
          Le système s'adapte automatiquement au patient le plus vulnérable.
        </p>
      </div>
    </div>
  );
}
