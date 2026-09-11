export default function SummaryCard({ title, value }) {
  return (
    <div className="card">
      <div style={{ color: '#64748b', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
        {title}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, marginTop: '0.5rem' }}>{value}</div>
    </div>
  );
}
