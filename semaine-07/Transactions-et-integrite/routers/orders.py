from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from email_service import send_confirmation_email
from models import Order, Product
from schemas import OrderCreate, OrderOut

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post(
    "",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    data: OrderCreate,
    session: AsyncSession = Depends(get_db),
) -> Order:
    try:
        async with session.begin():
            product = await session.get(
                Product,
                data.product_id,
            )

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Produit introuvable",
                )

            if product.stock < data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuffisant",
                )

            product.stock -= data.quantity

            order = Order(
                product_id=data.product_id,
                quantity=data.quantity,
            )

            session.add(order)

            await session.flush()

            await send_confirmation_email(order.id)

        return order

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la commande",
        ) from error