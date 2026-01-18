import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const page = Number(url.searchParams.get('page') ?? '1');

  const res = await fetch(`/api/raw-articles?page=${page}`);
  const json = await res.json();

  const totalPages = Math.ceil(json.total / json.page_size);

  return {
    data: json,
    page,
    totalPages
  };
};

