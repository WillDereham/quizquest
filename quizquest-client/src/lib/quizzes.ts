import { initializeApp, type FirebaseApp } from 'firebase/app'

const firebaseConfig = {
  apiKey: 'AIzaSyB9lD5c9njBsdKcVLgLNgTi5oxUcftTxBw',
  authDomain: 'quizquestgg.firebaseapp.com',
  projectId: 'quizquestgg',
  storageBucket: 'quizquestgg.appspot.com',
  messagingSenderId: '846649727856',
  appId: '1:846649727856:web:250e466877fa0dfe34cdb5',
}

let app: FirebaseApp | null

export interface Quiz {
  id: string
  title: string
  description: string
  default_time_limit: string
  created_at: { seconds: number; nanoseconds: number }
  last_updated: { seconds: number; nanoseconds: number }
  questions: unknown[]
}

export function getApp(): FirebaseApp {
  if (app) return app
  app = initializeApp(firebaseConfig)
  return app
}
