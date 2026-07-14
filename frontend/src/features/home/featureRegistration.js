import { createAuthActions } from '../../actions/authActions'
import { createInvoiceActions } from '../../actions/invoiceActions'
import { createPaymentActions } from '../../actions/paymentActions'
import ApplePayCheckoutCard from '../../components/payment/ApplePayCheckoutCard.vue'
import AuthCard from '../../components/payment/AuthCard.vue'
import FooterNote from '../../components/payment/FooterNote.vue'
import InvoicePreviewCard from '../../components/payment/InvoicePreviewCard.vue'
import InvoiceScannerCard from '../../components/payment/InvoiceScannerCard.vue'
import PaymentColumns from '../../components/payment/PaymentColumns.vue'
import PaymentHeroPanel from '../../components/payment/PaymentHeroPanel.vue'
import PaymentTimelineCard from '../../components/payment/PaymentTimelineCard.vue'
import { UI_COMPONENT_IDS, UI_SCREENS } from '../../core/uiElements'
import { defineFeature, defineRoute, defineScreen } from '../featureBuilders'
import { defineComponentSpec, defineSlot, defineSlots } from '../screenBuilders'
import { AuthService } from '../../services/authService'
import { InvoiceService } from '../../services/invoiceService'
import { PaymentService } from '../../services/paymentService'


export function createHomeFeatureRegistration() {
  return defineFeature({
    featureId: 'home',
    serviceFactories: {
      authService: (ctx) => new AuthService(ctx.service('apiGateway'), ctx.state),
      invoice: (ctx) => new InvoiceService(ctx.state),
      payment: (ctx) => new PaymentService(ctx.service('apiGateway'), ctx.state),
    },
    actionFactories: {
      auth: createAuthActions,
      invoice: createInvoiceActions,
      payment: createPaymentActions,
    },
    routeDefinitions: [
      defineRoute({
        path: '/',
        name: 'home',
        screen: UI_SCREENS.HOME,
      }),
    ],
    screenDefinitions: [
      defineScreen({
        screen: UI_SCREENS.HOME,
        onEnter: async ({ app }) => {
          if (app.action('auth').isAuthenticated()) {
            await app.action('payment').loadHistory()
          }
        },
        slots: defineSlots({
          header: defineSlot([
            defineComponentSpec({
              id: UI_COMPONENT_IDS.HOME_HERO,
              order: 10,
              component: PaymentHeroPanel,
              buildProps: ({ app }) => ({
                invoiceReady: Boolean(app.state.invoice.current),
                isAuthenticated: app.action('auth').isAuthenticated(),
                isDemoMode: app.state.payment.demoMode || app.state.config.demoMode,
                currentStep: app.action('payment').getCurrentStep(),
                onReset: () => app.action('invoice').clear(),
              }),
            }),
          ]),
          main: defineSlot([
            defineComponentSpec({
              id: UI_COMPONENT_IDS.HOME_SCANNER,
              order: 10,
              component: PaymentColumns,
              buildProps: ({ app }) => ({
                left: [
                  defineComponentSpec({
                    id: UI_COMPONENT_IDS.HOME_AUTH,
                    component: AuthCard,
                    props: {
                      authState: app.state.session,
                      authError: app.service('authService').lastError(),
                      onLogin: (usernameOrEmail, password) => app.action('auth').login(usernameOrEmail, password),
                      onRegister: (input) => app.action('auth').register(input),
                      onLogout: () => app.action('auth').logout(),
                    },
                  }),
                  defineComponentSpec({
                    id: UI_COMPONENT_IDS.HOME_SCANNER,
                    component: InvoiceScannerCard,
                    props: {
                      rawPayload: app.state.invoice.rawPayload,
                      onScan: (payload) => {
                        try {
                          app.action('invoice').parse(payload)
                        } catch {
                          return false
                        }
                        return true
                      },
                    },
                  }),
                  defineComponentSpec({
                    id: UI_COMPONENT_IDS.HOME_CHECKOUT,
                    component: ApplePayCheckoutCard,
                    props: {
                      invoice: app.state.invoice.current,
                      paymentState: app.state.payment,
                      isAuthenticated: app.action('auth').isAuthenticated(),
                      stripePublishableKey: app.state.config.stripePublishableKey,
                      createPaymentRequest: (invoice) => app.action('payment').createPaymentRequest(invoice),
                      confirmWalletPayment: (payload) => app.action('payment').confirmWalletPayment(payload),
                    },
                  }),
                ],
                right: [
                  defineComponentSpec({
                    id: UI_COMPONENT_IDS.HOME_PREVIEW,
                    component: InvoicePreviewCard,
                    props: {
                      invoice: app.state.invoice.current,
                      parseError: app.state.invoice.parseError,
                    },
                  }),
                  defineComponentSpec({
                    id: UI_COMPONENT_IDS.HOME_TIMELINE,
                    component: PaymentTimelineCard,
                    props: {
                      invoice: app.state.invoice.current,
                      payment: app.state.payment,
                      session: app.state.session,
                    },
                  }),
                ],
              }),
            }),
          ]),
          footer: defineSlot([
            defineComponentSpec({
              id: 'home.footer-note',
              order: 10,
              component: FooterNote,
            }),
          ]),
        }),
      }),
    ],
    testTargets: [
      'src/tests/screenRegistry.spec.js',
      'src/tests/authService.spec.js',
      'src/tests/invoiceParser.spec.js',
      'tests/pegger.e2e.spec.js',
      'tests/pegger.optical.spec.js',
    ],
  })
}
