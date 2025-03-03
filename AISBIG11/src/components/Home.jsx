
function Home(){
    return(
        <div className="h-screen flex flex-col ">
            <div className=" m-auto flex flex-col gap-6">
                <h1 className="sm:text-2xl">Welcome to AIS Big 11</h1>
                <h1 className="sm:text-8xl text-5xl">AIS<span className="sm:text-9xl text-6xl">BIG</span><span className="text-6xl">11</span></h1>
                <div className="flex sm:flex-row flex-col-reverse items-end gap-4 sm:gap-0 sm:justify-between">
                    <h1 className="underline ">See More&gt;&gt;</h1>
                    <h1>Universities and Authors Ranking</h1>
                </div>
                
            </div>
            <div className="flex justify-end bg-black text-white pt-10">
                <div className="pb-16 pr-20 sm:text-lg flex flex-col gap-3">
                    <div className="grid sm:grid-cols-2  ">
                        <h1 className="sm:w-1/2 sm:mx-auto hidden sm:block">Developed by:</h1>
                        <div>
                            <h1>Akmal Mirsadikov</h1>
                            <h1>W. Frank Barton School of Business</h1>
                            <h1>Wichita State University</h1>
                        </div>
                    </div>
                    <div className="grid sm:grid-cols-2 ">
                        <h1 className="sm:w-1/2 sm:mx-auto">Contact:</h1>
                        <a className="text-blue-gray-600 underline" href="mailto:akmal.mirsadikov@wichita.edu">akmal.mirsadikov@wichita.edu</a>
                    </div>
                </div>

            </div>
            
            
        </div>
    )
}
export default Home;