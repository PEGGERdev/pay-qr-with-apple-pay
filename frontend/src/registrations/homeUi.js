import { createScreenModule } from '../core/screenRegistry'
import { UI_COMPONENT_IDS, UI_SCREENS } from '../core/uiElements'
import AuthCard from '../components/payment/AuthCard.vue'
import InvoiceScannerCard from '../components/payment/InvoiceScannerCard.vue'
import InvoicePreviewCard from '../components/payment/InvoicePreviewCard.vue'
import ApplePayCheckoutCard from '../components/payment/ApplePayCheckoutCard.vue'
import PaymentTimelineCard from '../components/payment/PaymentTimelineCard.vue'
import PaymentHeroPanel from '../components/payment/PaymentHeroPanel.vue'
import PaymentColumns from '../components/payment/PaymentColumns.vue'
import FooterNote from '../components/payment/FooterNote.vue'

const homeScreen = createScreenModule(UI_SCREENS.HOME)

homeScreen.lifecycle({
  async onEnter({ app }) {
    if (app.controller('auth').isAuthenticated()) {
      await app.controller('payment').loadHistory()
    }
  },
})

homeScreen.header({
  id: UI_COMPONENT_IDS.HOME_HERO,
  order: 10,
  component: PaymentHeroPanel,
  buildProps: ({ app }) => ({
    invoiceReady: Boolean(app.state.invoice.current),
    isAuthenticated: app.controller('auth').isAuthenticated(),
    apiBaseUrl: app.state.config.apiBaseUrl,
    isDemoMode: app.state.payment.demoMode || app.state.config.demoMode,
    onReset: () => app.controller('invoice').clear(),
  }),
})

homeScreen.main({
  id: UI_COMPONENT_IDS.HOME_SCANNER,
  order: 10,
  component: PaymentColumns,
  buildProps: ({ app }) => ({
    left: [
      {
        id: UI_COMPONENT_IDS.HOME_AUTH,
        component: AuthCard,
        props: {
          authState: app.state.session,
          authError: app.service('authService').lastError(),
          onLogin: (usernameOrEmail, password) => app.controller('auth').login(usernameOrEmail, password),
          onRegister: (input) => app.controller('auth').register(input),
          onLogout: () => app.controller('auth').logout(),
        },
      },
      {
        id: UI_COMPONENT_IDS.HOME_SCANNER,
        component: InvoiceScannerCard,
        props: {
          onScan: (payload) => {
            try {
              app.controller('invoice').parse(payload)
            } catch {
              return false
            }
            return true
          },
        },
      },
      {
        id: UI_COMPONENT_IDS.HOME_CHECKOUT,
        component: ApplePayCheckoutCard,
        props: {
          invoice: app.state.invoice.current,
          paymentState: app.state.payment,
          isAuthenticated: app.controller('auth').isAuthenticated(),
          stripePublishableKey: app.state.config.stripePublishableKey,
          createPaymentRequest: (invoice) => app.controller('payment').createPaymentRequest(invoice),
          confirmWalletPayment: (payload) => app.controller('payment').confirmWalletPayment(payload),
        },
      },
    ],
    right: [
      {
        id: UI_COMPONENT_IDS.HOME_PREVIEW,
        component: InvoicePreviewCard,
        props: {
          invoice: app.state.invoice.current,
          parseError: app.state.invoice.parseError,
        },
      },
      {
        id: UI_COMPONENT_IDS.HOME_TIMELINE,
        component: PaymentTimelineCard,
        props: {
          invoice: app.state.invoice.current,
          payment: app.state.payment,
          session: app.state.session,
        },
      },
    ],
  }),
})

homeScreen.footer({
  id: 'home.footer-note',
  order: 10,
  component: FooterNote,
})
