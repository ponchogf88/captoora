import Foundation
import Vision
import AppKit
let args=CommandLine.arguments
var results:[[String:Any]]=[]
for path in args.dropFirst() {
 guard let image=NSImage(contentsOfFile:path),let cg=image.cgImage(forProposedRect:nil,context:nil,hints:nil) else{continue}
 let req=VNRecognizeTextRequest();req.recognitionLevel = .accurate;req.recognitionLanguages=["en-US","es-ES","fr-FR"];req.usesLanguageCorrection=false;req.minimumTextHeight=0.001
 do { try VNImageRequestHandler(cgImage:cg,options:[:]).perform([req]);let words=(req.results ?? []).compactMap{obs -> [String:Any]? in guard let t=obs.topCandidates(1).first, t.confidence>=0.25 else{return nil};let b=obs.boundingBox;return ["text":t.string,"confidence":t.confidence,"box":[b.minX*Double(cg.width),(1-b.maxY)*Double(cg.height),b.maxX*Double(cg.width),(1-b.minY)*Double(cg.height)]]};results.append(["path":path,"size":[cg.width,cg.height],"words":words]) } catch {results.append(["path":path,"error":String(describing:error)])}
}
let data=try JSONSerialization.data(withJSONObject:results,options:[.prettyPrinted,.sortedKeys]);FileHandle.standardOutput.write(data)
