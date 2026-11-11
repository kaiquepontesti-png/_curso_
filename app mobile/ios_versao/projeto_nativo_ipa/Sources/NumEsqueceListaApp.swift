import SwiftUI

@main
struct NumEsqueceListaApp: App {
    var body: some Scene {
        WindowGroup {
            WebViewContainer()
                .ignoresSafeArea()
                .preferredColorScheme(.light)
        }
    }
}
