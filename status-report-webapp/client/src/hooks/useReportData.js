import { useEffect, useState } from 'react';
import { fetchCurrentReport } from '../services/api';

export default function useReportData() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await fetchCurrentReport();
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return { report, loading, error, reload: load };
}
