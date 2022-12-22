import { getApp, type Quiz } from '$lib/quizzes'
import { collection, getDocs, getFirestore, orderBy, query } from 'firebase/firestore/lite'
import type { PageLoad } from './$types'

export const load = (async () => {
  const app = getApp()
  const db = getFirestore(app)
  const quizzes = await (
    await getDocs(query(collection(db, 'quizzes'), orderBy('last_updated')))
  ).docs.map((doc) => ({ id: doc.id, ...doc.data() } as Quiz))
  console.log(quizzes)
  return { quizzes }
}) satisfies PageLoad

export const ssr = false
