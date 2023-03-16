import {
  collection,
  doc,
  getDoc,
  getDocs,
  getFirestore,
  orderBy,
  query,
} from 'firebase/firestore/lite'
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
  default_time_limit: number
  created_at: { seconds: number; nanoseconds: number }
  last_updated: { seconds: number; nanoseconds: number }
  questions: unknown[]
}

export interface Question {
  id: string
  text: string
  time_limit: string | null
  answers: { id: string; correct: boolean; text: string }[]
}

function getApp(): FirebaseApp {
  if (app) return app
  app = initializeApp(firebaseConfig)
  return app
}

export async function getQuiz(quizId: string): Quiz | null {
  const app = getApp()
  const db = getFirestore(app)
  const quizSnap = await getDoc(doc(db, 'quizzes', quizId))
  return quizSnap.exists() ? ({ id: quizSnap.id, ...quizSnap.data() } as Quiz) : null
}

export async function getQuizList(): Quiz[] {
  const app = getApp()
  const db = getFirestore(app)
  const quizzes = await (
    await getDocs(query(collection(db, 'quizzes'), orderBy('last_updated', 'desc')))
  ).docs.map((doc) => ({ id: doc.id, ...doc.data() } as Quiz))
  return quizzes
}
