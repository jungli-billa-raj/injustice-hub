import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  const res = await fetch('/api/raw-articles?page=1');
  const data = await res.json();

  return {
    data
  };
};

