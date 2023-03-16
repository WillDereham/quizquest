import { getQuizList } from '$lib/quizzes'
import type { PageLoad } from './$types'

export const load = (async () => {
  return {
    quizzes: getQuizList(),
  }
}) satisfies PageLoad

export const ssr = false
