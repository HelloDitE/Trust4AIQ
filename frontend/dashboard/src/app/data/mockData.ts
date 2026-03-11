// Données mockées pour le système de supervision

export interface Patient {
  name: string;
  score: number;
  level: 'OPTIMAL' | 'MODÉRÉ' | 'ÉLEVÉ' | 'CRITIQUE';
}

export interface Pollutant {
  id: string;
  name: string;
  value: number;
  unit: string;
  threshold: number;
  status: 'Bon' | 'Moyen' | 'Mauvais';
  description: string;
  trend?: 'up' | 'down' | 'stable';
}

export interface Room {
  id: string;
  name: string;
  service: string;
  patientCount: number;
  globalScore: number;
  level: 'OPTIMAL' | 'MODÉRÉ' | 'ÉLEVÉ' | 'CRITIQUE';
  status: 'OPTIMAL' | 'VIGILANCE' | 'DANGER' | 'URGENCE';
  lastUpdate: string;
  patients: Patient[];
  criticalPatient: string;
  pollutants: Pollutant[];
  description: string;
  action: string;
}

export const rooms: Room[] = [
  {
    id: '203',
    name: 'Chambre 203',
    service: 'Réanimation',
    patientCount: 3,
    globalScore: 2.4,
    level: 'ÉLEVÉ',
    status: 'DANGER',
    lastUpdate: '15:05',
    patients: [
      { name: 'M. Dubois', score: 1.3, level: 'MODÉRÉ' },
      { name: 'M. Martin', score: 2.4, level: 'ÉLEVÉ' },
      { name: 'Mme Blanc', score: 1.1, level: 'MODÉRÉ' }
    ],
    criticalPatient: 'M. Martin',
    description: 'Le seuil de tolérance du patient le plus fragile est dépassé.',
    action: 'Mode BOOST – Ventilation maximale activée',
    pollutants: [
      {
        id: 'co2',
        name: 'CO₂',
        value: 1250,
        unit: 'ppm',
        threshold: 1000,
        status: 'Mauvais',
        description: 'Dioxyde de carbone',
        trend: 'up'
      },
      {
        id: 'pm25',
        name: 'PM2.5',
        value: 38,
        unit: 'µg/m³',
        threshold: 25,
        status: 'Mauvais',
        description: 'Particules fines',
        trend: 'up'
      },
      {
        id: 'no2',
        name: 'NO₂',
        value: 45,
        unit: 'µg/m³',
        threshold: 40,
        status: 'Moyen',
        description: 'Dioxyde d\'azote',
        trend: 'stable'
      },
      {
        id: 'cov',
        name: 'COV',
        value: 320,
        unit: 'µg/m³',
        threshold: 300,
        status: 'Moyen',
        description: 'Composés organiques volatils',
        trend: 'down'
      },
      {
        id: 'temperature',
        name: 'Température',
        value: 23,
        unit: '°C',
        threshold: 24,
        status: 'Bon',
        description: 'Température ambiante',
        trend: 'stable'
      },
      {
        id: 'humidity',
        name: 'Humidité',
        value: 52,
        unit: '%',
        threshold: 60,
        status: 'Bon',
        description: 'Humidité relative',
        trend: 'stable'
      }
    ]
  },
  {
    id: '204',
    name: 'Chambre 204',
    service: 'Réanimation',
    patientCount: 2,
    globalScore: 1.8,
    level: 'ÉLEVÉ',
    status: 'VIGILANCE',
    lastUpdate: '15:05',
    patients: [
      { name: 'Mme Dupont', score: 1.8, level: 'ÉLEVÉ' },
      { name: 'M. Leroux', score: 0.9, level: 'OPTIMAL' }
    ],
    criticalPatient: 'Mme Dupont',
    description: 'L\'air est techniquement conforme, mais le patient fragile commence à être exposé.',
    action: 'Mode CONFORT – Augmentation du débit d\'air de +20%',
    pollutants: [
      {
        id: 'co2',
        name: 'CO₂',
        value: 950,
        unit: 'ppm',
        threshold: 1000,
        status: 'Bon',
        description: 'Dioxyde de carbone',
        trend: 'stable'
      },
      {
        id: 'pm25',
        name: 'PM2.5',
        value: 22,
        unit: 'µg/m³',
        threshold: 25,
        status: 'Bon',
        description: 'Particules fines',
        trend: 'down'
      },
      {
        id: 'no2',
        name: 'NO₂',
        value: 28,
        unit: 'µg/m³',
        threshold: 40,
        status: 'Bon',
        description: 'Dioxyde d\'azote',
        trend: 'stable'
      },
      {
        id: 'cov',
        name: 'COV',
        value: 280,
        unit: 'µg/m³',
        threshold: 300,
        status: 'Bon',
        description: 'Composés organiques volatils',
        trend: 'stable'
      },
      {
        id: 'temperature',
        name: 'Température',
        value: 22,
        unit: '°C',
        threshold: 24,
        status: 'Bon',
        description: 'Température ambiante',
        trend: 'stable'
      },
      {
        id: 'humidity',
        name: 'Humidité',
        value: 48,
        unit: '%',
        threshold: 60,
        status: 'Bon',
        description: 'Humidité relative',
        trend: 'stable'
      }
    ]
  },
  {
    id: '205',
    name: 'Chambre 205',
    service: 'Réanimation',
    patientCount: 1,
    globalScore: 0.7,
    level: 'OPTIMAL',
    status: 'OPTIMAL',
    lastUpdate: '15:05',
    patients: [
      { name: 'M. Bernard', score: 0.7, level: 'OPTIMAL' }
    ],
    criticalPatient: 'M. Bernard',
    description: 'Conditions optimales. Aucune action requise.',
    action: 'Mode STANDARD – Fonctionnement normal',
    pollutants: [
      {
        id: 'co2',
        name: 'CO₂',
        value: 720,
        unit: 'ppm',
        threshold: 1000,
        status: 'Bon',
        description: 'Dioxyde de carbone',
        trend: 'stable'
      },
      {
        id: 'pm25',
        name: 'PM2.5',
        value: 12,
        unit: 'µg/m³',
        threshold: 25,
        status: 'Bon',
        description: 'Particules fines',
        trend: 'stable'
      },
      {
        id: 'no2',
        name: 'NO₂',
        value: 18,
        unit: 'µg/m³',
        threshold: 40,
        status: 'Bon',
        description: 'Dioxyde d\'azote',
        trend: 'stable'
      },
      {
        id: 'cov',
        name: 'COV',
        value: 180,
        unit: 'µg/m³',
        threshold: 300,
        status: 'Bon',
        description: 'Composés organiques volatils',
        trend: 'stable'
      },
      {
        id: 'temperature',
        name: 'Température',
        value: 21,
        unit: '°C',
        threshold: 24,
        status: 'Bon',
        description: 'Température ambiante',
        trend: 'stable'
      },
      {
        id: 'humidity',
        name: 'Humidité',
        value: 45,
        unit: '%',
        threshold: 60,
        status: 'Bon',
        description: 'Humidité relative',
        trend: 'stable'
      }
    ]
  },
  {
    id: '206',
    name: 'Chambre 206',
    service: 'Réanimation',
    patientCount: 2,
    globalScore: 1.4,
    level: 'MODÉRÉ',
    status: 'VIGILANCE',
    lastUpdate: '15:05',
    patients: [
      { name: 'Mme Petit', score: 1.4, level: 'MODÉRÉ' },
      { name: 'M. Moreau', score: 1.2, level: 'MODÉRÉ' }
    ],
    criticalPatient: 'Mme Petit',
    description: 'L\'air est techniquement conforme, mais le patient fragile commence à être exposé.',
    action: 'Mode CONFORT – Augmentation du débit d\'air de +20%',
    pollutants: [
      {
        id: 'co2',
        name: 'CO₂',
        value: 880,
        unit: 'ppm',
        threshold: 1000,
        status: 'Bon',
        description: 'Dioxyde de carbone',
        trend: 'stable'
      },
      {
        id: 'pm25',
        name: 'PM2.5',
        value: 28,
        unit: 'µg/m³',
        threshold: 25,
        status: 'Moyen',
        description: 'Particules fines',
        trend: 'up'
      },
      {
        id: 'no2',
        name: 'NO₂',
        value: 35,
        unit: 'µg/m³',
        threshold: 40,
        status: 'Bon',
        description: 'Dioxyde d\'azote',
        trend: 'stable'
      },
      {
        id: 'cov',
        name: 'COV',
        value: 290,
        unit: 'µg/m³',
        threshold: 300,
        status: 'Bon',
        description: 'Composés organiques volatils',
        trend: 'stable'
      },
      {
        id: 'temperature',
        name: 'Température',
        value: 22,
        unit: '°C',
        threshold: 24,
        status: 'Bon',
        description: 'Température ambiante',
        trend: 'stable'
      },
      {
        id: 'humidity',
        name: 'Humidité',
        value: 50,
        unit: '%',
        threshold: 60,
        status: 'Bon',
        description: 'Humidité relative',
        trend: 'stable'
      }
    ]
  }
];

export const getServiceStats = () => {
  const totalRooms = rooms.length;
  const roomsInDanger = rooms.filter(r => r.status === 'DANGER' || r.status === 'URGENCE').length;
  const roomsInVigilance = rooms.filter(r => r.status === 'VIGILANCE').length;
  const roomsOptimal = rooms.filter(r => r.status === 'OPTIMAL').length;

  return {
    totalRooms,
    roomsInDanger,
    roomsInVigilance,
    roomsOptimal
  };
};
