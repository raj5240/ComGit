import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { compareAPI } from '../services/api'

const Dashboard = () => {
    const [url1, setUrl1] = useState('')
    const [url2, setUrl2] = useState('')
    const [comparison, setComparison] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const user = JSON.parse(localStorage.getItem('user') || '{}')

    const handleLogout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        navigate('/login')
    }

    const handleCompare = async (e) => {
        e.preventDefault()
        setError('')
        setComparison(null)
        setLoading(true)

        try {
            const response = await compareAPI.compare(url1, url2)
            setComparison(response.comparison_text)
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to compare profiles. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const formatComparisonText = (text) => {
        const lines = text.split('\n')
        const elements = []
        let listItems = []
        let listKey = 0

        const flushList = () => {
            if (listItems.length > 0) {
                elements.push(
                    <ul key={`ul-${listKey++}`} className="list-disc ml-6 mb-4 space-y-1">
                        {listItems}
                    </ul>
                )
                listItems = []
            }
        }

        const formatBoldText = (content) => {
            const parts = content.split(/(\*\*.*?\*\*)/g)
            return parts.map((part, idx) => {
                if (part.startsWith('**') && part.endsWith('**')) {
                    return <strong key={idx}>{part.slice(2, -2)}</strong>
                }
                return <span key={idx}>{part}</span>
            })
        }

        lines.forEach((line, index) => {
            if (line.startsWith('# ')) {
                flushList()
                elements.push(
                    <h1 key={`h1-${index}`} className="text-3xl font-bold mt-6 mb-4 text-gray-800">
                        {line.substring(2)}
                    </h1>
                )
            } else if (line.startsWith('## ')) {
                flushList()
                elements.push(
                    <h2 key={`h2-${index}`} className="text-2xl font-bold mt-5 mb-3 text-gray-700">
                        {line.substring(3)}
                    </h2>
                )
            } else if (line.startsWith('### ')) {
                flushList()
                elements.push(
                    <h3 key={`h3-${index}`} className="text-xl font-semibold mt-4 mb-2 text-gray-700">
                        {line.substring(4)}
                    </h3>
                )
            } else if (line.startsWith('- ')) {
                const content = line.substring(2)
                listItems.push(
                    <li key={`li-${index}`} className="text-gray-700">
                        {formatBoldText(content)}
                    </li>
                )
            } else if (line.startsWith('**') && line.endsWith(':**')) {
                flushList()
                const boldText = line.replace(/\*\*/g, '')
                elements.push(
                    <p key={`p-bold-${index}`} className="font-semibold mt-3 mb-2 text-gray-700">
                        {boldText}
                    </p>
                )
            } else if (line.trim()) {
                flushList()
                elements.push(
                    <p key={`p-${index}`} className="mb-2 text-gray-600">
                        {formatBoldText(line)}
                    </p>
                )
            }
        })

        flushList()
        return elements
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-indigo-600">GitHub Profile Comparator</h1>
                        </div>
                        <div className="flex items-center space-x-4">
                            <span className="text-gray-700">Welcome, {user.username}</span>
                            <button
                                onClick={handleLogout}
                                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-6">Compare GitHub Profiles</h2>

                    <form onSubmit={handleCompare} className="space-y-4">
                        <div>
                            <label htmlFor="url1" className="block text-sm font-medium text-gray-700 mb-2">
                                First GitHub Profile URL
                            </label>
                            <input
                                type="url"
                                id="url1"
                                value={url1}
                                onChange={(e) => setUrl1(e.target.value)}
                                required
                                placeholder="https://github.com/username1"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label htmlFor="url2" className="block text-sm font-medium text-gray-700 mb-2">
                                Second GitHub Profile URL
                            </label>
                            <input
                                type="url"
                                id="url2"
                                value={url2}
                                onChange={(e) => setUrl2(e.target.value)}
                                required
                                placeholder="https://github.com/username2"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>

                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                        >
                            {loading ? 'Comparing...' : 'Compare Profiles'}
                        </button>
                    </form>
                </div>

                {comparison && (
                    <div className="bg-white rounded-lg shadow-xl p-8">
                        <div className="prose max-w-none">
                            {formatComparisonText(comparison)}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Dashboard

