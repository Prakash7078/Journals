import { Navbar } from "@material-tailwind/react"
import Home from "./components/Home"
import { BrowserRouter, Routes, Route } from "react-router-dom"
function App() {
  
  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="/details" element={<Navbar/>}></Route>
      </Routes>
      </BrowserRouter>
      
    </div>
  )
}

export default App
