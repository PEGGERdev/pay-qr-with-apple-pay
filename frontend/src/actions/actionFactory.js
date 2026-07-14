function normalizeArgs(args) {
  return Array.from(args || [])
}


export function createActionGroup(ctx, definitions) {
  return Object.fromEntries(
    Object.entries(definitions).map(([actionName, actionDefinition]) => [
      actionName,
      (...args) => actionDefinition({ ctx, args: normalizeArgs(args) }),
    ]),
  )
}


export function defineServiceAction({ serviceId, method, after }) {
  return async ({ ctx, args }) => {
    const result = await ctx.service(serviceId)[method](...args)
    if (typeof after === 'function') {
      await after({ ctx, args, result })
    }
    return result
  }
}


export function defineStateAction(handler) {
  return ({ ctx, args }) => handler({ ctx, args })
}
