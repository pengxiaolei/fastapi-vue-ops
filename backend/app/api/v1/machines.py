from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiRequest, ApiResponse
from app.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
    MachineListResponse,
    ConnectionTestRequest,
    ConnectionTestResponse,
    MachineStatusResponse,
)
from app.services.machine_service import MachineService

router = APIRouter()


@router.post("", response_model=ApiResponse[MachineListResponse])
async def machine_operations(
    request: ApiRequest[dict],
    db: Session = Depends(get_db),
):
    """
    机器管理统一入口

    action 功能标识:
    - machine.list: 获取机器列表
    - machine.get: 获取机器详情
    - machine.create: 创建机器
    - machine.update: 更新机器
    - machine.delete: 删除机器
    - machine.test_connection: 测试连接（不保存）
    - machine.test_saved_connection: 测试已保存机器连接
    - machine.refresh_status: 刷新机器状态
    - machine.add_tag: 添加标签到机器
    - machine.remove_tag: 移除机器标签
    - machine.add_to_group: 添加机器到分组
    - machine.remove_from_group: 从分组移除机器
    """
    action = request.action
    data = request.data or {}

    # 获取机器列表
    if action == "machine.list":
        page = data.get("page", 1)
        page_size = data.get("page_size", 20)
        keyword = data.get("keyword")
        status = data.get("status")
        environment = data.get("environment")

        skip = (page - 1) * page_size
        machines, total = MachineService.get_machines(
            db, skip=skip, limit=page_size, keyword=keyword,
            status=status, environment=environment
        )

        result = MachineListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
            data=machines
        )
        return ApiResponse.ok(data=result, action=action)

    # 获取机器详情
    elif action == "machine.get":
        machine_id = data.get("id")
        machine = MachineService.get_machine(db, machine_id)
        return ApiResponse.ok(data=machine, action=action)

    # 创建机器
    elif action == "machine.create":
        machine_data = MachineCreate(**data)
        machine = MachineService.create_machine(db, machine_data)
        return ApiResponse.ok(data=machine, message="创建成功", action=action)

    # 更新机器
    elif action == "machine.update":
        machine_id = data.get("id")
        update_data = MachineUpdate(**{k: v for k, v in data.items() if k != "id"})
        machine = MachineService.update_machine(db, machine_id, update_data)
        return ApiResponse.ok(data=machine, message="更新成功", action=action)

    # 删除机器
    elif action == "machine.delete":
        machine_id = data.get("id")
        MachineService.delete_machine(db, machine_id)
        return ApiResponse.ok(message="删除成功", action=action)

    # 测试连接（不保存）
    elif action == "machine.test_connection":
        conn_request = ConnectionTestRequest(**data)
        success, message, sys_info = MachineService.test_connection(
            hostname=conn_request.hostname,
            port=conn_request.port,
            username=conn_request.username,
            auth_type=conn_request.auth_type,
            password=getattr(conn_request, "password", None),
            private_key=getattr(conn_request, "private_key", None),
        )

        result = ConnectionTestResponse(
            success=success,
            message=message,
            **sys_info
        )
        return ApiResponse.ok(data=result, action=action)

    # 测试已保存机器连接
    elif action == "machine.test_saved_connection":
        machine_id = data.get("id")
        success, message, sys_info = MachineService.test_machine_connection(db, machine_id)
        result = ConnectionTestResponse(
            success=success,
            message=message,
            **sys_info
        )
        return ApiResponse.ok(data=result, action=action)

    # 刷新机器状态
    elif action == "machine.refresh_status":
        machine_id = data.get("id")
        success, message = MachineService.refresh_machine_status(db, machine_id)
        machine = MachineService.get_machine(db, machine_id)
        result = MachineStatusResponse(
            success=success,
            message=message,
            status=machine.status if machine else None,
            cpu_usage=machine.cpu_usage if machine else None,
            memory_usage=machine.memory_usage if machine else None,
            disk_usage=machine.disk_usage if machine else None,
        )
        return ApiResponse.ok(data=result, action=action)

    # 添加标签到机器
    elif action == "machine.add_tag":
        machine_id = data.get("machine_id")
        tag_id = data.get("tag_id")
        MachineService.add_tag_to_machine(db, machine_id, tag_id)
        return ApiResponse.ok(message="添加标签成功", action=action)

    # 移除机器标签
    elif action == "machine.remove_tag":
        machine_id = data.get("machine_id")
        tag_id = data.get("tag_id")
        MachineService.remove_tag_from_machine(db, machine_id, tag_id)
        return ApiResponse.ok(message="移除标签成功", action=action)

    # 添加机器到分组
    elif action == "machine.add_to_group":
        machine_id = data.get("machine_id")
        group_id = data.get("group_id")
        MachineService.add_machine_to_group(db, machine_id, group_id)
        return ApiResponse.ok(message="添加到分组成功", action=action)

    # 从分组移除机器
    elif action == "machine.remove_from_group":
        machine_id = data.get("machine_id")
        group_id = data.get("group_id")
        MachineService.remove_machine_from_group(db, machine_id, group_id)
        return ApiResponse.ok(message="从分组移除成功", action=action)

    else:
        return ApiResponse.error(message=f"未知的操作类型: {action}", code=400, action=action)
