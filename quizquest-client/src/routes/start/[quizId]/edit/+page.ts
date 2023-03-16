import { getQuiz } from '$lib/quizzes'
import type { PageLoad } from './$types'
import { error } from '@sveltejs/kit'

export const load = (async ({ params: { quizId } }) => {
  const quiz = await getQuiz(quizId)
  if (!quiz) throw error(404, { message: 'Quiz not found' })
  return { quiz }
}) satisfies PageLoad

export const ssr = false
