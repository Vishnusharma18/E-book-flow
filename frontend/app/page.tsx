'use client';

import { useState, useEffect } from 'react';

interface Project {
  id: string;
  title: string;
  topic_or_url: string;
  status: string;
  progress: number;
  current_step: string;
}

export default function DashboardPage() {
  const [topic, setTopic] = useState('');
  const [title, setTitle] = useState('');
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchProjects = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/projects');
      if (res.ok) {
        const data = await res.json();
        setProjects(data);
      }
    } catch (err) {
      console.log('Backend connection offline or starting...');
    }
  };

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic_or_url: topic, title: title.trim() || undefined }),
      });
      if (res.ok) {
        setTopic('');
        setTitle('');
        fetchProjects();
      }
    } catch (err) {
      alert('Failed to initiate book project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-12">
      {/* Create New Book Section */}
      <section className="bg-white p-8 rounded-2xl border border-stone-200 shadow-sm">
        <h2 className="text-2xl font-serif text-stone-900 mb-2">Create New Automated Publishing Suite</h2>
        <p className="text-stone-600 font-sans text-sm mb-6">
          Enter a concept, biography topic, or URL to generate a complete 10-chapter book, print PDF, EPUB 3.0, 3D mockups, and sales landing page.
        </p>

        <form onSubmit={handleCreate} className="space-y-4 font-sans">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-stone-700 uppercase tracking-wider mb-1">
                Book Concept or Topic URL *
              </label>
              <input
                type="text"
                placeholder="e.g. Life of Marcus Aurelius or Renaissance Masters"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500 bg-stone-50"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-stone-700 uppercase tracking-wider mb-1">
                Custom Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Meditations on Stoic Courage"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500 bg-stone-50"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full md:w-auto px-8 py-3 bg-stone-900 hover:bg-stone-800 text-amber-50 font-medium rounded-lg shadow transition duration-200"
          >
            {loading ? 'Initializing Agent Pipeline...' : 'Generate Publishing Bundle'}
          </button>
        </form>
      </section>

      {/* Real-time Task Progress Dashboard */}
      <section className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-serif text-stone-900">Active Publishing Projects</h2>
          <span className="text-xs font-sans text-stone-500">{projects.length} Total Projects</span>
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl border border-stone-200 text-stone-500 font-sans text-sm">
            No projects found. Create one above to launch the AI publishing pipeline!
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {projects.map((proj) => (
              <div key={proj.id} className="bg-white p-6 rounded-xl border border-stone-200 shadow-sm space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-serif text-stone-900">{proj.title}</h3>
                    <p className="text-xs text-stone-500 font-sans mt-1">Topic/Context: {proj.topic_or_url}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-sans uppercase tracking-wider font-semibold ${
                    proj.status === 'completed' ? 'bg-emerald-100 text-emerald-800' :
                    proj.status === 'failed' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {proj.status}
                  </span>
                </div>

                {/* Progress Bar */}
                <div className="space-y-2 font-sans">
                  <div className="flex justify-between text-xs text-stone-600">
                    <span>{proj.current_step}</span>
                    <span>{Math.round(proj.progress)}%</span>
                  </div>
                  <div className="w-full bg-stone-100 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-amber-600 h-full transition-all duration-500"
                      style={{ width: `${proj.progress}%` }}
                    />
                  </div>
                </div>

                {/* Download / Action buttons */}
                {proj.status === 'completed' && (
                  <div className="flex flex-wrap gap-4 pt-2 font-sans text-sm">
                    <a
                      href={`http://localhost:8000/api/projects/${proj.id}/download`}
                      className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg shadow font-medium transition"
                    >
                      Download .ZIP Bundle
                    </a>
                    <a
                      href={`http://localhost:8000/api/projects/${proj.id}/landing`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-stone-100 hover:bg-stone-200 text-stone-800 rounded-lg border border-stone-300 font-medium transition"
                    >
                      View Sales Landing Page
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
